import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='yadirconv',
      version='1.0.3',
      description='Получение статистики по конверсиям из Яндекс Директа в разрезе кампаний, таргетингов, ОС, пола и возраста',
      packages=['yadirconv'],
      author="Lubiviy Alexander",
      author_email='lybiviyalexandr@gmail.com',
      url="https://vk.com/lubiviy_alexander",
                 )