from io import StringIO
from ruamel.yaml import YAML
import asyncio


yaml = YAML(typ="safe")


async def kubectl_apply(spec, context):
    cmd = [
        "kubectl",
        "apply",
        "--wait",  # Wait for objects to be 'ready' before returning
        "-f",
        "-",
    ]
    if context:
        cmd.append(f"--context={context}")
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    with StringIO() as s:
        yaml.dump_all(spec, s)
        s.seek(0)
        objs = s.read()
    self.log.debug(f"kubectl applying {objs}")
    stdout, stderr = await proc.communicate(objs.encode())

    if (await proc.wait()) != 0:
        raise ValueError(f"kubectl apply failed: {stdout}, {stderr}")
