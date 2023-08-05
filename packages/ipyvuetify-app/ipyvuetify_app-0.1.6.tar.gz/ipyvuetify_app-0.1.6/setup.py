# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ipyvuetify_app']

package_data = \
{'': ['*']}

install_requires = \
['char>=0.1.2,<0.2.0', 'ipyvuetify>=1.8.1,<2.0.0', 'ipywidgets>=7.6.5,<8.0.0']

setup_kwargs = {
    'name': 'ipyvuetify-app',
    'version': '0.1.6',
    'description': '',
    'long_description': '===================\nipyvuetify_app\n===================\n\n.. image:: https://img.shields.io/github/last-commit/stas-prokopiev/ipyvuetify_app\n   :target: https://img.shields.io/github/last-commit/stas-prokopiev/ipyvuetify_app\n   :alt: GitHub last commit\n\n.. image:: https://img.shields.io/github/license/stas-prokopiev/ipyvuetify_app\n    :target: https://github.com/stas-prokopiev/ipyvuetify_app/blob/master/LICENSE.txt\n    :alt: GitHub license<space><space>\n\n.. image:: https://img.shields.io/pypi/v/ipyvuetify_app\n   :target: https://img.shields.io/pypi/v/ipyvuetify_app\n   :alt: PyPI\n\n.. image:: https://img.shields.io/pypi/pyversions/ipyvuetify_app\n   :target: https://img.shields.io/pypi/pyversions/ipyvuetify_app\n   :alt: PyPI - Python Version\n\n\n.. contents:: **Table of Contents**\n\nShort Overview.\n=========================\nipyvuetify_app is a python package (**py>=3.7**) with a simple template for writing ipyvuetify application\n\nExamples how your app can look like\n----------------------------------------\n\n|pic1| |pic2|\n\n.. |pic1| image:: images/light_1.PNG\n   :height: 300px\n\n.. |pic2| image:: images/dark_1.PNG\n   :height: 300px\n\nApplication from the box supports theme switcher and navigation over different content by menus on top\n\nA few more examples how header navigation works\n------------------------------------------------\n\n|pic3| |pic4|\n\n.. |pic3| image:: images/light_menu_opened.png\n   :height: 300px\n\n.. |pic4| image:: images/light_too_many_menu_items.PNG\n   :height: 300px\n\nInstallation via pip:\n======================\n\n.. code-block:: bash\n\n    pip install ipyvuetify_app\n\nHow to use it\n===========================\n\n| To create an application by the given template you need to create a routing class\n| That will be in charge of what to show in the main application section\n| For every selected menu item -> subitem\n| Then you just give the router to **ipyvuetify_app.VueApp(...)** and it does all the magic for you\n\n.. code-block:: python\n\n    from ipyvuetify_app import VueApp\n    from ipyvuetify_app import VueAppRouter\n\n    vue_app_router_example = VueAppRouter()\n    VueApp(vue_app_router_example)\n\n\nHow to write a Router\n----------------------\n\n| Every router should satisfy 2 conditions:\n| 1) It has method **get_main_content(self, item, subitem)** which should return page\'s main content\n| 2) It has attribute **self.dict_list_subitems_by_item** with all subitems for every menu item\n\nSimple Router example\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n.. code-block:: python\n\n    class VueAppRouter():\n\n        def __init__(self):\n            self.dict_list_subitems_by_item = {}\n            for item in range(5):\n                list_subitems = [str(subitem) for subitem in range(item, 5 + item)]\n                self.dict_list_subitems_by_item[str(item)] = list_subitems\n\n        def get_main_content(self, item, subitem):\n            return f"{item} -> {subitem}"\n\n\nFull VuaApp signature\n----------------------\n\n.. code-block:: python\n\n    VueApp(\n        vue_app_router,\n        list_vw_fab_app_bar_left=None,\n        list_vw_fab_app_bar_right=None,\n        list_footer_vw_children=None,\n    )\n\nArguments:\n\n#. **list_vw_fab_app_bar_left**:\n    | List with ipyvuetify fab icon buttons to put on the left side of Application Header Bar\n#. **list_vw_fab_app_bar_right**:\n    | List with ipyvuetify fab icon buttons to put on the right side of Application Header Bar\n#. **list_footer_vw_children**:\n    | List with ipyvuetify widgets to put in the footer\n    | If empty then footer is not shown at all\n\n\nVuaApp object description\n--------------------------------------------\n\nVuaApp is a child of v.App so it has all the parent methods and attributes\n\nUseful Attributes:\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n#. **self.vw_appbar**:\n    | v.AppBar(app=True, ...) - Application top bar\n#. **self.vw_navigation_drawer**:\n    | v.NavigationDrawer(app=True, ...) - Navigation Drawer at the left side\n#. **self.vw_app_main**:\n    | v.Content() - Main section of the application\n#. **self.vw_footer**:\n    | v.Footer(app=True, ...) - Footer of the application\n\n\nUseful Methods:\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n#. **self.update_app_routing()**:\n    | When router items were updated please call this method to update application menus\n\nLinks\n=====\n\n    * `PYPI <https://pypi.org/project/ipyvuetify_app/>`_\n    * `GitHub <https://github.com/stas-prokopiev/ipyvuetify_app>`_\n\nProject local Links\n===================\n\n    * `CHANGELOG <https://github.com/stas-prokopiev/ipyvuetify_app/blob/master/CHANGELOG.rst>`_.\n    * `CONTRIBUTING <https://github.com/stas-prokopiev/ipyvuetify_app/blob/master/CONTRIBUTING.rst>`_.\n\nContacts\n========\n\n    * Email: stas.prokopiev@gmail.com\n    * `vk.com <https://vk.com/stas.prokopyev>`_\n    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_\n\nLicense\n=======\n\nThis project is licensed under the MIT License.',
    'author': 'stanislav',
    'author_email': 'stas.prokopiev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stas-prokopiev/ipyvuetify_app',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
