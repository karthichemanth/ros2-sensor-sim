from setuptools import find_packages, setup

package_name = 'sensor_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='Temperature sensor simulator',
    license='MIT',
    entry_points={
        'console_scripts': [
            'publisher = sensor_sim.temperature_publisher:main',
            'subscriber = sensor_sim.temperature_subscriber:main',
        ],
    },
)