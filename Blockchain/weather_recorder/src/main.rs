// Import necessary modules
use solana_client::rpc_client::RpcClient;
use solana_sdk::{
    instruction::{AccountMeta, Instruction},
    pubkey::Pubkey,
    signature::{Keypair, Signer},
    system_program,
    transaction::Transaction,
};
use serde::{Deserialize};
use paho_mqtt::{AsyncClient, ConnectOptions, Message, QoS};
use std::time::Duration;
use tokio; // Import tokio for async/await support

// Define a module for configuration
mod config;

// Define a struct to hold sensor data
#[derive(Deserialize)]
struct SensorData {
    temperature: f64,
    humidity: f64,
}

// Define the main function as async
#[tokio::main]
async fn main() {
    // Get the RPC URL from the configuration
    let rpc_url = config::RPC_URL;
    // Get the program ID from the configuration
    let program_id = Pubkey::from_str(config::PROGRAM_ID).unwrap();
    // Create a new RPC client
    let client = RpcClient::new(rpc_url);
    // Create a new keypair for the payer
    let payer = Keypair::new();

    // Get the MQTT username and password from the configuration
    let mqtt_username = config::MQTT_USERNAME;
    let mqtt_password = config::MQTT_PASSWORD;
    // Get the MQTT URL from the configuration
    let mqtt_url = config::MQTT_URL;
    // Get the MQTT topic from the configuration
    let topic = config::MQTT_TOPIC;
    // Set the QoS level for the MQTT subscription
    let qos = QoS::AtLeastOnce;

    // Create a new MQTT client
    let mut mqtt_options = ConnectOptions::new();
    mqtt_options.set_username(mqtt_username);
    mqtt_options.set_password(mqtt_password);
    let (mut mqtt_client, _) = AsyncClient::new(mqtt_url).unwrap();
    // Connect to the MQTT broker
    mqtt_client.connect(mqtt_options).await.unwrap();
    // Subscribe to the MQTT topic
    mqtt_client.subscribe(topic, qos).await.unwrap();

    // Start consuming messages from the MQTT topic
    let mut stream = mqtt_client.start_consuming().await.unwrap();
    while let Some(msg) = stream.next().await {
        if let Ok(msg) = msg {
            // Deserialize the message payload into a SensorData struct
            if let Ok(data) = serde_json::from_slice::<SensorData>(&msg.payload()) {
                // Create a new keypair for the weather account
                let weather_account = Keypair::new();
                // Create a new instruction for the program
                let instruction = create_instruction(program_id, data, payer.pubkey(), weather_account.pubkey());
                // Create a new transaction for the instruction
                let transaction = create_transaction(instruction, payer.pubkey());
                // Get the recent blockhash from the RPC client
                let recent_blockhash = client.get_recent_blockhash().unwrap().0;
                // Sign the transaction with the payer and weather account keypairs
                transaction.sign(&[&payer, &weather_account], recent_blockhash);
                // Send and confirm the transaction on the Solana network
                client.send_and_confirm_transaction(&transaction).unwrap();
                // Print a message to the console indicating that the data has been recorded
                println!("Recorded: Temp: {} Humidity: {}", data.temperature, data.humidity);
            }
        }
    }
}

// Function to create a new instruction for the program
fn create_instruction(program_id: Pubkey, data: SensorData, payer: Pubkey, weather_account: Pubkey) -> Instruction {
    // Create a new instruction with the program ID, data, and account metadata
    Instruction::new_with_bincode(
        program_id,
        &(data.temperature, data.humidity),
        vec![
            AccountMeta::new(payer, true),
            AccountMeta::new(weather_account, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
    )
}

// Function to create a new transaction for the instruction
fn create_transaction(instruction: Instruction, payer: Pubkey) -> Transaction {
    // Create a new transaction with the instruction and payer
    Transaction::new_with_payer(&[instruction], Some(&payer))
}