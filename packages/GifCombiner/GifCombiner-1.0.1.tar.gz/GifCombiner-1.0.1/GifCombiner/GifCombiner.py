import glob
from PIL import Image #PIL은 pip install이 필요함

class GifCombiner:
    
    """
    여러 장의 이미지를, 순차적으로 나타나는 하나의 GIF 이미지(움짤)로 바꿔주는 클래스
    """
    
    def __init__(self,path_in = None,path_out = None, resize = (320,240)):
        """[summary]

        Args:
            path_in : 여러 장의 이미지가 있는 경로
            path_out : 결과 이미지 저장 경로
            resize : 리사이징 크기.(default = (320,480))
        """
        
        self.path_in = path_in or './*.png'
        #path_in이 없다면 현재 경로의 png파일을 모두 들고옴
        #에러를 최소화하기 위함 / glob에 의해 가능한 것
        self.path_out = path_out or './output.gif'
        self.resize = resize
        
    def combine_gif(self):
        """
        GIF 이미지 변환 기능 수행
        """
        
        #경로, 사이즈 확인
        print(f'path_in : {self.path_in}\npath_out : {self.path_out},resize : {self.resize}')
        
        img,*images = [Image.open(f).resize((320,240),Image.ANTIALIAS) for f in sorted(glob.glob(self.path_in))]
        #패킹활용. 첫번째 이미지는 img에, 나머지는 모두 패킹해서 images로 넣어줌
        #glob을 활용해 path_in경로에 있는 모든 것들을 가져옴
        
        try:
            img.save(
                fp=self.path_out, #output경로
                format = "GIF", #output파일 포멧
                append_images = images, #image에 추가할 image들
                save_all=True,
                duration = 500,#전환속도
                loop = 0#반복횟수
            )
        except IOError:
            print("Cannot convert!",img)    
    
#test            
if __name__ == "__main__":
    c = GifCombiner("./project/images/*.png","project/image_out/result.gif",(320,240))
    c.combine_gif()
        