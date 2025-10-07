import asyncio
from prefect import flow, task


@task
async def greet_user(name: str):
    await asyncio.sleep(5)  # Simulating a delay
    return f"Hello, {name}!\n"


@task
async def provide_status_update(name: str):
    await asyncio.sleep(6)  # Simulating a delay
    return f"{name}, your current status is: Active\n"


@task
async def fetch_account_balance(name: str):
    await asyncio.sleep(7)  # Simulating a longer delay
    return f"{name}, your account balance is: $1,234.56\n"


# Asynchronous Flow
@flow
async def user_notification_async_flow(user_name: str):
    # Trigger the tasks to run in parallel (asynchronous execution)
    greeting_task = greet_user(user_name)
    status_task = provide_status_update(user_name)
    balance_task = fetch_account_balance(user_name)

    result = await asyncio.gather(
        greet_user(user_name),
        provide_status_update(user_name),
        fetch_account_balance(user_name)
    )

    final_message = "".join(result)
    return final_message


if __name__ == "__main__":
    # Asynchronous execution demo
    print("Asynchronous Flow (Tasks run in parallel):")
    result_async = asyncio.run(user_notification_async_flow("John"))
    print(result_async)
