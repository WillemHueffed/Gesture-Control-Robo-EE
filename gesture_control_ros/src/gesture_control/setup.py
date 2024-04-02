from setuptools import setup

package_name = 'gesture_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='locobot',
    maintainer_email='willmhueffed@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gesture_recognizer = gesture_control.gesture_recognizer:main',
            'command_translator = gesture_control.command_translator:main',
            'video_display = gesture_control.video_display:main',
            'camera_feed = gesture_control.camera_feed:main'
        ],
    },
)
