from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="CsuModels",  # 这里是pip项目发布的名称
    version="1.0.26",  # 版本号，数值大的会优先被pip
    keywords=["pip", "csu", "models"],
    # description="word",
    license="MIT Licence",
    author="csu_ywj",
    packages=find_packages(),
    # data_files=['PMTD/maskrcnn_benchmark/_C.cpython-36m-x86_64-linux-gnu.so'],
    include_package_data=True,
    platforms="any",
    install_requires=["ninja==1.10.2.3", "yacs==0.1.8", "cython==0.29.22", "matplotlib==3.3.4", "tqdm==4.62.3",
                      "pyclipper==1.3.0.post2", "Keras==2.3.1", "tensorflow-gpu==1.15.2", "numpy==1.16.0",
                      "opencv-python==3.4.4.19", "scikit-learn==0.21.2","scipy==1.1.0", "Pillow",
                      "torch==1.3.0", "torchvision==0.4.1", "CsuSort==1.0.14", "CsuPMTD==1.0.26"]
)
