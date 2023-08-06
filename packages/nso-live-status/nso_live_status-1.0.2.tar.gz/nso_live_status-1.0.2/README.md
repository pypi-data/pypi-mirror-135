# nso_live_status
This library is an example on how you can retrieve raw cli with Cisco NSO and parse the result with pyats/genie parser.

> this code only works with cli based NEDs

# Installation

```
pip install nso-live-status
```
# Usage
In an NSO Action let's say you want to check the version of your devices.

In the python code of the package you will use it like this :

```python
import ncs
from nso_live_status import run_live_status
from distutils.version import LooseVersion
from ncs.dp import Action


CHECK_OK = "OK"
CHECK_NOK = "NOK"
CHECK_ERROR = "ERROR"


class CheckVersion(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output, trans):
        self.log.info(f"Action CheckVersion , device : {input.device} target version : {input.target_version}")
        command = "show version"
        root = ncs.maagic.get_root(trans)

        show_version = run_live_status(root, input.device, command)

        target_version = LooseVersion(input.target_version)
        if show_version.has_structured_output:
            current_version = LooseVersion(show_version.structured_output["software_version"])
            if current_version == target_version:
                output.check_status = CHECK_OK
                output.check_message = f"[check_version] Current version of the device {current_version} match the target version {target_version}"
            else:
                output.check_status = CHECK_NOK
                output.check_message = f"[check_version] Current version of the device {current_version} doesn't match the target version {target_version}"
        else:
            output.check_status = CHECK_ERROR
            output.check_message = f"[check_version] ERROR unable to retrieve structured output from {input.device} with the command {command}"
```
run_live_status will populate and return this dataclass :
```python
@dataclass()
class CommandResult:
    has_error: bool = False
    raw_cli: str = ""
    structured_output: str = ""

    @property
    def has_structured_output(self):
        try:
            if len(self.structured_output) > 0:
                return True
            else:
                return False
        except TypeError:
            return False
```

If a pyats parser is found for the cli command you will find a dict in *structured_output* 



- Commands supported : https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers
- OS platform and model supported : https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/supported_platforms.html#/
    

## License

This project is licensed to you under the terms of the [Cisco Sample Code License](https://raw.githubusercontent.com/rtrjl/nso_restconf/master/LICENSE).
