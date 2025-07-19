from setuptools import setup, find_packages

setup(
    name="LensifiedSelfie",
    version="0.1.0",
    author="Amir",
    description="Animate sunglasses on faces with AI-powered eye detection",
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "PySide6",
        "numpy",
        "opencv-python",
        "dlib",      
    ],
    entry_points={
        "console_scripts": [
            "lensify=lensify.pipeline:main", 
        ],
    },
    include_package_data=True,
)
