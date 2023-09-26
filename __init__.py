# import logging
# import os

<<<<<<< HEAD
# from .plugin import JLCPCBPlugin

# # logging.basicConfig(
# #     level=logging.DEBUG,
# #     format="%(asctime)s [%(levelname)s] %(message)s",
# #     handlers=[
# #         logging.FileHandler(
# #             os.path.join(os.path.dirname(os.path.realpath(__file__)), "debug.log")
# #         ),
# #         logging.StreamHandler(),
# #     ],
# # )

# # LOGGER = logging.getLogger()

# # try:
# JLCPCBPlugin().register()
# # except Exception as e:
# # LOGGER.debug(repr(e))
=======
from .plugin import JLCPCBPlugin

# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s [%(levelname)s] %(message)s",
#     handlers=[
#         logging.FileHandler(
#             os.path.join(os.path.dirname(os.path.realpath(__file__)), "debug.log")
#         ),
#         logging.StreamHandler(),
#     ],
# )

# LOGGER = logging.getLogger()

# try:
JLCPCBPlugin().register()
# except Exception as e:
# LOGGER.debug(repr(e))
>>>>>>> 8c28854a5b5a1b75a5564260e35eb43f135b6937
