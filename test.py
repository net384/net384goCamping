import c_GetCampDay 
import requests
import json
import inspect

print(inspect.getfile(requests))


class MyClass:
    class_variable = 0  # 클래스 변수

    def __init__(self, instance_variable):
        self.instance_variable = instance_variable  # 인스턴스 변수

    def update_class_variable(self, value):
        MyClass.class_variable = value

# 객체 생성
obj1 = MyClass("Instance 1")
obj2 = MyClass("Instance 2")

# 클래스 변수와 클래스 속성 값 확인
print("Class Variable:", MyClass.class_variable)  # 출력: Class Variable: 0
print("Instance 1:", obj1.instance_variable)      # 출력: Instance 1
print("Instance 2:", obj2.instance_variable)      # 출력: Instance 2

# 클래스 변수 업데이트
obj1.update_class_variable(5)
print("Class Variable after update:", MyClass.class_variable)  

print(obj1.class_variable)
print(obj2.class_variable)


class Circle:
    def __init__(self, radius):
        self._radius = radius

    def get_radius(self):
        return self._radius

    def set_radius(self, value):
        if value >= 0:
            self._radius = value
        else:
            print("Radius must be a non-negative value")

    def get_area(self):
        return 3.14 * self._radius * self._radius

    # 프로퍼티를 정의하지 않고 메서드를 호출하는 방법
    radius = property(get_radius, set_radius)
    area = property(get_area)

# 객체 생성
circle = Circle(5)

# 속성처럼 메서드 사용
print("Radius:", circle.radius)  # 출력: Radius: 5
print("Area:", circle.area)      # 출력: Area: 78.5

# 프로퍼티를 통한 값 변경
circle.radius = 7
print("New Radius:", circle.radius)  # 출력: New Radius: 7

circle.radius = -2  # 유효하지 않은 값
# 출력: Radius must be a non-negative value



class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value >= 0:
            self._radius = value
        else:
            print("Radius must be a non-negative value")

    @property
    def area(self):
        return 3.14 * self._radius * self._radius

# 객체 생성
circle = Circle(5)

# 속성처럼 프로퍼티 사용
print("Radius:", circle.radius)  # 출력: Radius: 5
print("Area:", circle.area)      # 출력: Area: 78.5

# 프로퍼티를 통한 값 변경
circle.radius = 7
print("New Radius:", circle.radius)  # 출력: New Radius: 7

circle.radius = -2  # 유효하지 않은 값
# 출력: Radius must be a non-negative value