from setuptools import setup

setup(
      name='v2x_sdk',
      version='0.1',
      description='An sdk that for the V2X data',
      long_description='An sdk that pulls data from the V2X dataset.',
      author='Ben Davis',
      author_email="bdavis@hra.com",
      packages=['v2x_sdk'],
      install_requires=["boto3","requests", "pandas", "python-keycloak","requests==2.25.1", "urllib3==1.26.5"],
      zip_safe=True,
      python_requires='>=3.7.3'
)
