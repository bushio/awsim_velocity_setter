from setuptools import setup

package_name = 'vehicle_inputs_setter'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='satoshi',
    maintainer_email='satoshi@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'vel_keyboard_setter = vehicle_inputs_setter.vel_keyboard_setter:main',
            'vel_throttle_setter = vehicle_inputs_setter.vel_throttle_setter:main',
        ],
    },
)
