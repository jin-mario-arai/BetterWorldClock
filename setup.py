from setuptools import setup

setup(
    app=['wc.py'],
    name="Better World Clock",
    version="0.0.1",
    options={
        "py2app": {
            "includes": ["os", "platform"],
            "semi_standalone": True,
        }
    },
)