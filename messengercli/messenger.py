#!/usr/bin/env python3
"""
@Author: King
@Date: 2023-05-03 21:46:45
@Email: linsy_king@sjtu.edu.cn
"""

import typer
import os
import shutil
import json

app = typer.Typer(add_completion=False)


class Messenger:
    config = None

    def __init__(self) -> None:
        """
        Check if `messager.json` exists and load it.
        """
        if os.path.exists("messenger.json"):
            with open("messenger.json", "r") as f:
                self.config = json.load(f)
        else:
            raise Exception(
                "messenger.json not found. Are you in the project initialized by the Messenger? Try `messenger init <your-project-name>`."
            )

    def dump_config(self):
        with open("messenger.json", "w") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def add_scene(self, name: str):
        if name in self.config["scenes"]:
            raise Exception("Scene already exists.")
        self.config["scenes"][name] = []
        self.dump_config()
        os.mkdir(f"src/Scenes/{name}")

    def update_scenes(self):
        """
        Update scene settings (AllScenes and SceneSettings)
        """
        scenes = [x for x in self.config["scenes"]]
        with open(".messenger/Templates/scene/Scenes/AllScenes.elm", "r") as f:
            content = f.read()
        dol0 = "\n".join(
            [
                f"import Scenes.{l}.Export as {l}\nimport Scenes.{l}.Global as {l}G"
                for l in scenes
            ]
        )
        dol1 = ",\n".join([f'( "{l}", {l}G.sceneToST {l}.scene )' for l in scenes])
        content = content.replace("$0", dol0).replace("$1", dol1)
        # Write
        with open("src/Scenes/AllScenes.elm", "w") as f:
            f.write(content)

        dol0 = "\n".join([f"import Scenes.{l}.Export as {l}" for l in scenes])

        dol1 = "\n    | ".join([f"{l}DataT {l}.Data" for l in scenes])
        with open(".messenger/Templates/scene/Scenes/SceneSettings.elm", "r") as f:
            content = f.read()
        content = content.replace("$0", dol0).replace("$1", dol1)
        # Write
        with open("src/Scenes/SceneSettings.elm", "w") as f:
            f.write(content)

    def update_rep(self, file_proto, file_output, dollar, rep):
        with open(file_proto, "r") as f:
            content = f.read()
        content = content.replace(f"${dollar}", rep)
        # Write
        with open(file_output, "w") as f:
            f.write(content)

    def update_rep_next(self, file_output, dollar, rep):
        with open(file_output, "r") as f:
            content = f.read()
        content = content.replace(f"${dollar}", rep)
        # Write
        with open(file_output, "w") as f:
            f.write(content)

    def add_component(self, name: str):
        """
        Add a component
        """
        os.mkdir(f"src/Components/{name}")
        self.update_rep(
            ".messenger/Templates/component/Components/Sample/Sample.elm",
            f"src/Components/{name}/{name}.elm",
            0,
            name,
        )
        self.update_rep(
            ".messenger/Templates/component/Components/Sample/Export.elm",
            f"src/Components/{name}/Export.elm",
            0,
            name,
        )

    def format(self):
        os.system("elm-format src/ --yes")

    def add_layer(self, scene: str, layer: str):
        """
        Add a layer to a scene
        """
        if scene not in self.config["scenes"]:
            raise Exception("Scene doesn't exist.")
        self.config["scenes"][scene].append(layer)
        self.dump_config()
        os.mkdir(f"src/Scenes/{scene}/{layer}")
        self.update_rep(
            ".messenger/Templates/layer/Sample/Model.elm",
            f"src/Scenes/{scene}/{layer}/Model.elm",
            0,
            scene,
        )
        self.update_rep_next(
            f"src/Scenes/{scene}/{layer}/Model.elm",
            1,
            layer,
        )
        self.update_rep(
            ".messenger/Templates/layer/Sample/Global.elm",
            f"src/Scenes/{scene}/{layer}/Global.elm",
            0,
            scene,
        )
        self.update_rep_next(
            f"src/Scenes/{scene}/{layer}/Global.elm",
            1,
            layer,
        )
        self.update_rep(
            ".messenger/Templates/layer/Sample/Export.elm",
            f"src/Scenes/{scene}/{layer}/Export.elm",
            0,
            scene,
        )
        self.update_rep_next(
            f"src/Scenes/{scene}/{layer}/Export.elm",
            1,
            layer,
        )
        self.update_rep(
            ".messenger/Templates/layer/Sample/Common.elm",
            f"src/Scenes/{scene}/{layer}/Common.elm",
            0,
            f"{scene}.{layer}",
        )

    def update_layers(self):
        """
        Update layer settings.
        """
        for scene in self.config["scenes"]:
            layers = self.config["scenes"][scene]
            self.update_rep(
                ".messenger/Templates/scene/Scenes/Sample/Common.elm",
                f"src/Scenes/{scene}/Common.elm",
                0,
                scene,
            )
            self.update_rep(
                ".messenger/Templates/scene/Scenes/Sample/Export.elm",
                f"src/Scenes/{scene}/Export.elm",
                0,
                scene,
            )
            self.update_rep(
                ".messenger/Templates/scene/Scenes/Sample/Global.elm",
                f"src/Scenes/{scene}/Global.elm",
                0,
                scene,
            )
            self.update_rep(
                ".messenger/Templates/scene/Scenes/Sample/LayerBase.elm",
                f"src/Scenes/{scene}/LayerBase.elm",
                0,
                scene,
            )
            self.update_rep(
                ".messenger/Templates/scene/Scenes/Sample/LayerSettings.elm",
                f"src/Scenes/{scene}/LayerSettings.elm",
                0,
                scene,
            )
            self.update_rep_next(
                f"src/Scenes/{scene}/LayerSettings.elm",
                1,
                "\n".join([f"import Scenes.{scene}.{l}.Export as {l}" for l in layers]),
            )
            self.update_rep_next(
                f"src/Scenes/{scene}/LayerSettings.elm",
                2,
                "\n    | ".join([f"{l}Data {l}.Data" for l in layers]),
            )
            self.update_rep(
                ".messenger/Templates/scene/Scenes/Sample/Model.elm",
                f"src/Scenes/{scene}/Model.elm",
                0,
                scene,
            )
            self.update_rep_next(
                f"src/Scenes/{scene}/Model.elm",
                1,
                "\n".join(
                    [
                        f"import Scenes.{scene}.{l}.Export as {l}\nimport Scenes.{scene}.{l}.Global as {l}G"
                        for l in layers
                    ]
                ),
            )
            self.update_rep_next(
                f"src/Scenes/{scene}/Model.elm",
                2,
                ",\n".join(
                    [
                        f"""( "{l}"
          , let
                x =
                    {l}.layer
            in
            {l}G.getLayerCT {{ x | data = {l}.layer.init t NullLayerMsg initCommonData }}
          )"""
                        for l in layers
                    ]
                ),
            )


@app.command()
def init(
    name: str,
    use_full: bool = typer.Option(
        True,
        prompt="""Thanks for using Messenger.
There are currently two main versions you can use.
The core version only has the basic framework. There are no core engine support. Use this version if you want to create your own game engine.
The full version includes a core engine template which has a basic 2D physics engine and high-performance game component support. It enables you to create a level quickly.
See more instructions on https://github.com/linsyking/Messenger.git
Do you want to install the full version of Messerger?""",
    ),
):
    if use_full:
        version = "full"
        print("The full version is not supported yet...")
        exit(0)
    else:
        version = "core"
    input(
        f"""Here is my plan:
- Create a directory named {name}
- Use the {version} Messenger version
- Elm install the packages needed
Press Enter to continue
"""
    )
    os.makedirs(name, exist_ok=True)
    os.chdir(name)
    os.system(
        f"git clone https://github.com/linsyking/Messenger.git .messenger --depth=1"
    )
    shutil.copytree(".messenger/Templates/core/", "./src")
    shutil.copytree(".messenger/Templates/public/", "./public")
    shutil.copy(".messenger/Templates/.gitignore", "./.gitignore")
    shutil.copy(".messenger/Templates/Makefile", "./Makefile")
    shutil.copy(".messenger/Templates/elm.json", "./elm.json")

    os.makedirs("src/Scenes", exist_ok=True)
    os.makedirs("assets", exist_ok=True)
    os.makedirs("src/Components", exist_ok=True)

    print("Creating elm.json...")
    initObject = {
        "scenes": {},
        "components": {},
        "gamecomponents": {},
    }
    with open("messenger.json", "w") as f:
        json.dump(initObject, f, indent=4, ensure_ascii=False)
    print("Installing dependencies...")
    os.system("elm make")
    print("Done!")
    print(f"Now please go to {name} and add scenes and components.")


@app.command()
def component(name: str):
    msg = Messenger()
    input(f"You are going to create a component named {name}, continue?")
    msg.add_component(name)
    msg.format()
    print("Done!")


@app.command()
def scene(name: str):
    msg = Messenger()
    input(f"You are going to create a scene named {name}, continue?")
    msg.add_scene(name)
    msg.update_scenes()
    msg.format()
    print("Done!")


@app.command()
def layer(scene: str, layer: str):
    msg = Messenger()
    input(
        f"You are going to create a layer named {layer} under scene {scene}, continue?"
    )
    msg.add_layer(scene, layer)
    msg.update_layers()
    msg.format()
    print("Done!")


if __name__ == "__main__":
    app()