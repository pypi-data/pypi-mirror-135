# Picovoice Shepherd

Made in Vancouver, Canada by [Picovoice](https://picovoice.ai)

Picovoice Shepherd is the first no-code platform for building voice interfaces on microcontrollers.
It enables creating voice experiences similar to Alexa that run entirely on microcontrollers. 
Picovoice Shepherd accelerates prototyping, mitigates technical risks, and shortens time to market. 
Paired with [Picovoice Console](https://console.picovoice.ai/) users can deploy custom voice models into microcontrollers instantly.

## Compatibility

- Linux (x86_64)
- macOS (x86_64)
- Windows (x86_64)

## Supported Boards

- [STM32F407G-DISC1](https://www.st.com/en/evaluation-tools/stm32f4discovery.html)
- [STM32F411E-DISCO](https://www.st.com/en/evaluation-tools/32f411ediscovery.html)
- [STM32F469I-DISCO](https://www.st.com/en/evaluation-tools/32f469idiscovery.html)
- [STM32F769I-DISCO](https://www.st.com/en/evaluation-tools/32f769idiscovery.html)
- [STM32H735G-DK](https://www.st.com/en/evaluation-tools/stm32h735g-dk.html)
- [STM32H747I-DISCO](https://www.st.com/en/evaluation-tools/stm32h747i-disco.html)
- [i.MX RT1050 EVKB](https://www.nxp.com/design/development-boards/i-mx-evaluation-and-development-boards/i-mx-rt1050-evaluation-kit:MIMXRT1050-EVK)

## Installation

Install the Picovoice Shepherd:

```shell
pip3 install pvshepherd
```

### Note for macOS

Install Python using either the [official installer](https://www.python.org/downloads/mac-osx/) or [Homebrew](https://brew.sh).
Shepherd cannot run using the Python shipped with macOS. 
If using the Homebrew Python, make sure that `/usr/local/bin` is in the `PATH` variable before installing Shepherd.

### Note for Windows

The default Python installation options do not add it to the Windows `PATH` variable.
To fix the issue, refer to the [Python Docs](https://docs.python.org/3/using/windows.html#setting-envvars).

## Usage

Run the following command from the terminal:

```shell
pvshepherd
```

> On Linux, Shepherd will ask for the root password only on the first launch.

For more information, please refer to [Picovoice Shepherd Documentation](https://picovoice.ai/docs/picovoice-shepherd/)
