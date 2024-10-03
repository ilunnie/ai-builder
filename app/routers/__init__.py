import os
import pkgutil

from fastapi import APIRouter

package_dir = os.path.dirname(__file__)

routers = []
for _, name, _ in pkgutil.iter_modules([package_dir]):
    module = __import__(name, locals(), globals(), level=1)
    router = getattr(module, 'router', APIRouter())
    if isinstance(router, APIRouter):
        routers.append(router)
        
del os
del pkgutil
del APIRouter