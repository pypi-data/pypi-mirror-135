from setuptools import setup, Distribution


class BinaryDistribution(Distribution):
    def has_ext_modules(foo):
        return True
setup(
    name='xerier',
    version='0.0.1',
    packages=['xerier'],
    package_data={
        'xerier': ['xerier.so'],
    },
    distclass=BinaryDistribution,
    license='MIT'
)
