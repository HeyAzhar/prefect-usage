import asyncio
from prefect import flow, task


@task
async def fetch_user_info(user_id: int):
    await asyncio.sleep(2)  # Simulate fetching user data
    return {"user_id": user_id, "name": "John Doe"}


@task
async def check_account_balance(user_info: dict):
    await asyncio.sleep(3)  # Simulate checking account balance
    return f"{user_info['name']}, your account balance is: $1,234.56"


@task
async def send_notification(balance_info: str):
    await asyncio.sleep(1)  # Simulate sending email notification
    return f"Notification sent: {balance_info}"


@task
async def update_user_preferences(user_info: dict):
    await asyncio.sleep(2)  # Simulate updating preferences
    return f"Preferences updated for {user_info['name']}"

# Flow to demonstrate both dependent and parallel execution


@flow
async def user_account_flow(user_id: int):
    # Step 1: Fetch user info (this must happen first)
    user_info = await fetch_user_info(user_id)

    # Step 2 & 4: Run account balance check and preferences update in parallel
    balance_info, preferences_result = await asyncio.gather(
        check_account_balance(user_info),
        update_user_preferences(user_info)
    )

    # Step 3: Send notification (depends on balance check being complete)
    notification_result = await send_notification(balance_info)

    # Return final result combining both outcomes
    return f"{notification_result}\n{preferences_result}"

if __name__ == "__main__":
    # Run the async flow
    result = asyncio.run(user_account_flow(101))
    print(result)
