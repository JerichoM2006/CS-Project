import asyncio
import concurrent.futures

# Define a function to read input from the user
def blocking_input(prompt):
    return input(prompt)

async def asyncInput(prompt):
    # Use a thread pool to run the blocking input function
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        # Run the blocking input function in a separate thread
        return await loop.run_in_executor(pool, blocking_input, prompt)