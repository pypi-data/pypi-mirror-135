from setuptools import setup

setup(name='prom_client_sc',
      version='0.2',
      description='Python wrapper for prometheus client',
      url='https://github.com/ShareChat/python-prometheus-client',
      author='Sanket',
      author_email='souravmaitra@sharechat.co',
      packages=['python_prom_client'],
      install_requires=[
          'prometheus-client'
      ],
      setup_requires=['setuptools'],
      zip_safe=False)

