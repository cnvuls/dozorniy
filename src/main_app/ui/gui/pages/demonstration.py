import flet as ft

from ui.gui.components.feature_form import FeatureForm
from ui.gui.components.feature_list import FeatureList
from ui.gui.pages import featuremenu


class DemonstrationPage(ft.Container):
    def __init__(self):  # feature_form: FeatureForm, feature_list: FeatureList
        super().__init__()

        # self.feature_form = feature_form
        # self.feature_list = feature_list
        self.demonstration = ft.Image(
            src="./ui/gui/assets/asset.jpg",
            width=1280,
            height=720,
            fit=ft.BoxFit.CONTAIN,
            border_radius=6,
            gapless_playback=True,
        )

        self.content = self.demonstration
