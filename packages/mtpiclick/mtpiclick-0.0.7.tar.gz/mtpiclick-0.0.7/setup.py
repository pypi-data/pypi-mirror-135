from setuptools import setup, find_packages
setup(
    author="Patrick Toohey",
    description="HMI automation tools.",
    name="mtpiclick",
    version="0.0.7",
    packages=find_packages(include=["mtpiclick","mtpiclick.*"]),
    install_requires=['pyautogui', 'pywinauto'],
    python_requires='>=3.7',
)