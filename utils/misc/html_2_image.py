import logging
from typing import Dict
from .templates_mixin import TemplatesMixin
from data.config import TEMPLATES_DIR, WKHTMLTOIMAGE
import imgkit
from io import StringIO


class StandingsRenderer(TemplatesMixin):
    TEMPLATES_DIR = TEMPLATES_DIR

    def make_img(self, template_body: str, path_to_img: str):
        config: imgkit.config.Config = imgkit.config(
            wkhtmltoimage=WKHTMLTOIMAGE)

        html_table: str = self.render(
            'standings.tmpl',
            msg=template_body,
        )

        options: Dict[str, str] = {
            "format": "jpg",
            "quiet": "",
            "zoom": "3",
            "width": "1440",
            "disable-smart-width": "",
            "quality": "100",
        }
        try:
            imgkit.from_file(
                StringIO(html_table), path_to_img, config=config, options=options
            )
        except Exception as e:
            logging.e(e)
