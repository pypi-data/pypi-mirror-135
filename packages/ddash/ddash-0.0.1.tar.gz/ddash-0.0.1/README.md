# DDash

## Purposes
`docker` and `docker-compose` cli tool, to specify and automatic apply with current work directory.

## Installation
```bash
pip install ddash
```

## Instruction
- This program is using __stdout__ and __stderr__ which means it's able to support the next level deployment scripting.

- Setup following variable in you enviroment to make it permanently:
    + __DDASH_TIMEOUT__: Execute cli timeout [default is None(never timeout)]
    + __DDASH_PROJECT_DELIMITER__: Project delimiter for extracting prefix [default: `_`(underscore)]
    + __DDASH_PROJECT_SPLIT_LIMIT__: Project prefix word number for extracting prefix [default: 1]
    + __DDASH_ROOT_PATH__: Workspace [default: $HOME]
    + __DDASH_SUB_PATH__: Group directory combine with `ROOT_PATH`, `{PREFIX}` will be replace with porject prefix
    + __DDASH_SATELLITE_SUFFIX__: Satellite container name [default: service]
    + __DDASH_COMPOSE_FILENAME__: docker-compose filename [default: docker-compose.yml]
    + __DDASH_DOCKER_EXEC_COMMAND__: docker exec command [default: bash]

## Command
- `ps`: List running containers, format table and grep rows
- `launch`: Launch satellite container through project {PREFIX} which is extract from `$PWD` or --project, combine {SUFFIX} to up a satellite container [default: `{PREFIX}_service`]
- `terminate`: Terminate satellite container through project {PREFIX} which is extract from `$PWD` or --project, combine {SUFFIX} to up a satellite container [default: `{PREFIX}_service`]
- `up`: up container through project {PREFIX} which is extract from `$PWD` or --project, combine {SUFFIX} to up a satellite container [default: `{PREFIX}_service`]
- `down`: down container through project {PREFIX} which is extract from `$PWD` or --project, combine {SUFFIX} to up a satellite container [default: `{PREFIX}_service`]
- `run`: exec container with interactive tty mode through project {PREFIX} which is extract from `$PWD` or --project, combine {SUFFIX} to up a satellite container [default: `{PREFIX}_service`]

## Update Logs
|#|      date|version|
|-|----------|-------|
|1|2022/01/20| v0.0.0|

## 0.0.0
- Add the following commands:
    + ps
    + launch
    + terminate
    + up
    + down
    + run

If you like my work, please consider buying me a coffee or [PayPal](https://paypal.me/RonDevStudio?locale.x=zh_TW)
Thanks for your support! Cheers! 🎉
<a href="https://www.buymeacoffee.com/ronchang" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" align="right"></a>

