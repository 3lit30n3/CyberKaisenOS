from setuptools import setup, find_packages

setup(
    name="cyberkaisen",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scikit-learn",
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "cyberkaisen=cyberkaisen.cli.cyberkaisen_cli:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="CyberKaisenOS - Advanced Cybersecurity System with Phixeo Optimization",
    keywords="cybersecurity, virtualization, AI, honeypot, phixeo, sacred geometry",
    python_requires=">=3.6",
)
