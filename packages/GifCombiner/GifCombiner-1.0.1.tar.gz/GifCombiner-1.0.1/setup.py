from setuptools import setup, find_packages

setup(
    name             = 'GifCombiner', #수정해줘야함
    version          = '1.0.1',
    description      = 'Test package for distribution', #설명
    author           = 'EungBbin', #만든사람
    author_email     = 'colock123@gmail.com',
    url              = '',#패키지를 설명하는 사이트홈피
    download_url     = '',#다운로드형태로 제공
    install_requires = ['pillow'],
    #반드시 함께 필요한 애들 > 우리는 PILLOW를썼으니까 같이 적어준다 > 여기적혀있으면 패키지설치시 자동설치됨
    #참고로 glob은 내장함수라 설치안해도돼서 안적어준 것임
	include_package_data=True,
	packages=find_packages(), #패키지를 찾는 경로. 안적어두면 그냥 현재 경로에서 파일을 찾음. 현재경로에 패키지를 놔두면 그냥 바로 사용가능
    keywords         = ['GIFCONVERTER', 'gifconverter'],
    #검색할떄, 이 키워드로 검색하면 우리가 올려놓은게 검색이 됨
    python_requires  = '>=3', #필요파이썬 버전
    
    zip_safe=False,
    classifiers      = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]#어떤 환경에서 사용가능한지 ex)프로그래밍언어 : 파이썬, os는 윈도우..
    #https://pypi.org/classifiers/ 여기서 찾아서 가져와서 사용함
    
) 