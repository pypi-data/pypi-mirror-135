CLASS_TYPE_NAME = 'clsnm'
HASHCODE_ENCODING = 'utf-8'

# config = mx.get_parameterConfig('test1')
# config.daycounter = mx.Actual365Fixed()
# config.interpolationType = mx.InterpolateID.Linear

# calendar info (default calender)
# 
# calendar는 어케함...? 
'''
로드방식
user 가 뭔가를 해야함.
repo에 calendar setting? 을 할수가 있나.
아니면 어디에다가 놓아야하지

1. 따로 스크립트를 만들어서, 매번 사용할 때에 적용함

2. repo에서 날짜를 불러와서 이용함

속도는 1,2번 둘다 같음.

3. 다른방법이 있나...? - online에서 관리해 줌...?
   calendar를 내려받음.
   mxdevtool config server를 하나 돌려.
   거기서 calendar및 다른것들을 내려받어...?
   이건 repository 쪽이 있으면 거기서 update를 수행함.
   built in된 calender가 있고, 거기서 +- 형태가 나을듯.
   그리고 custom calendar도 있고
   그러면 파일이
   settings - calendar - built-in - [southkorea, us, japan, ]
                       - user     - [cal1, cal2]
            
   built-in 은 repository 에 하드코딩으로 박혀있음.
   그래서 초기에 repositoory를 만들면 이걸 토대로 만듬.
   또는 만들 필요가 없고, 기본만 있다가, web으로 부터 update?
   mxdevtool.exe 를 만들어서 update를 하는 건가 이런식. 
   이거는 생각보다 일이 커짐? 할게 많음...
   지금은 우선 repository에 더하고 빼는 거만.

   add 하고 하는 것들은 repository를 통해서 넣고 뺌.



목적 : 
사용자 calender를 이용할수가 있음. 잘 보고 세팅할수가 있음...?
그냥 repository에 따른 설정으로 감. 그러면 손쉽게 바꿀수가 있음.





'''
