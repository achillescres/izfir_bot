from loader import dp

from .big_brother import BigBrother


if __name__ == 'middlewares':
    dp.middleware.setup(BigBrother())
