import asyncio


def get_user_input(domain_name: str) -> str:
    return domain_name


async def nmap_scan(domain_name: str):
    cmd = f"nmap -p 80,443 {domain_name}"
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()
    print(f"Standard Output: {stdout.decode()}")
    return stdout

if __name__ == "__main__":
    nmap_scan("google.com")
