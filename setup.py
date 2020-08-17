from setuptools import setup

package_name = 'ros2pkg_ogameasure'

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
    maintainer='telescopio',
    maintainer_email='telescopio@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'e8257d='+package_name+'.Agilent.E8257:main',
            'pmx18_2a='+package_name+'.KIKUSUI.PMX18:main',
            'xffts='+package_name+'.RPG.xffts.main',

        ],
    },
)
