use anchor_lang::prelude::*;

declare_id!("88ro5Veod2sqYifwWbDnmFJXKgpHjMFtxZvT7Xos2qHp");

#[program]
pub mod weather_data {
    use super::*;

    pub fn record_data(ctx: Context<RecordData>, temperature: f64, humidity: f64) -> Result<()> {
        let weather_account = &mut ctx.accounts.weather_data;
        weather_account.temperature = temperature;
        weather_account.humidity = humidity;
        Ok(())
    }
}

#[derive(Accounts)]
pub struct RecordData<'info> {
    #[account(init, payer = user, space = 8 + 16)]
    pub weather_data: Account<'info, WeatherData>,
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[account]
pub struct WeatherData {
    pub temperature: f64,
    pub humidity: f64,
}