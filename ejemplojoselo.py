# Ejemplo python:
from abc import ABC, abstractmethod
from datetime import datetime


class Personaje(ABC):
    @abstractmethod
    def HacerRuido(self):
        pass

class PersonajeMovible(Personaje):
    @abstractmethod
    def mover(self):
        pass
class PersonajeEstatico(Personaje):
    @abstractmethod
    def fijarposicion(self):
        pass
class Mario(PersonajeMovible):

    def mover(self):
        pass

    def HacerRuido(self):
        pass

#
# lista: [Personaje] = [PersonajeMovible(), PersonajeEstatico()]
# p1 = PersonajeMovible()
# p1.

class Animal(ABC):
    @abstractmethod
    def HacerRuido(self):
        pass

    @abstractmethod
    def comer(self):
        pass

    @abstractmethod
    def getDescription(self):
        pass


class Gato(Animal):
    def getDescription(self):
        return "Gato"

    def comer(self):
        print("Comer carne")

    def HacerRuido(self):
        print("Miau")

class Perro(Animal):
    def comer(self):
        print("Alimento balanceado")

    def HacerRuido(self):
        print("wof")

    def getDescription(self):
        return "Perro"


class Loro(Animal):
    def comer(self):
        print("Comer mote")

    def HacerRuido(self):
        print("ahh")

    def getDescription(self):
        return "Loro"


class Elefante(Animal):
    def HacerRuido(self):
        print("Brrrr")

    def comer(self):
        print("come hierbas")

    def getDescription(self):
        return "Elefante"

class Header:
    def __init__(self, date: datetime, code: str, logo: str):
        self.date = date
        self.code = code
        self.logo = logo
    def toString(self):
        dateasStr = self.date.strftime( "%Y-%m-%d %H:%M:%S")
        return f"Header: \n {dateasStr} \n Code: {self.code} \n"


class BillingInformation:
    def __init__(self, company, name, address, phone, email):
        self.email = email
        self.phone = phone
        self.address = address
        self.name = name
        self.company = company

    def toString(self):
        return f"Billing Info: \n Email: {self.email} \n Phone: {self.phone} \n"


class ShippingInformation:
    def toString(self):
        return "No tengo informacion"


class Product(ABC):
    description = None
    quantity = None
    unitprice = 0
    
    @abstractmethod
    def getTotal(self):
        pass

class ProductSinDescuento(Product):
    def __init__(self, quantity: int, unitprice: float):
        self.unitprice = unitprice
        self.quantity = quantity

    def getTotal(self):
        return self.quantity * self.unitprice


class ProductEnpromocion(Product):
    def __init__(self, quantity: int, unitprice: float, discount: float):
        self.unitprice = unitprice
        self.discount = discount

    def getTotal(self):
        return self.quantity * self.unitprice * 0.5
        
class Factura:
    header = None
    billingInformation = None
    shippingInformation = None
    details: [Product] = []
    def addHeader(self, header: Header):
        self.header = header

    def addBillingInformation(self, billingInformation: BillingInformation):
        self.billingInformation = billingInformation

    def addShippingInformation(self, shippingInformation: ShippingInformation):
        self.shippingInformation = shippingInformation

    def addDetail(self, product: Product):
        self.details.append(product)

    def toString(self) -> str:
        return f"{self.header.toString()} \n {self.billingInformation.toString()} \n {self.shippingInformation.toString()}"


if __name__ == '__main__':
    # animales: [Animal] = [Gato(), Perro(), Loro(), Elefante()]
    #
    # for animal in animales:
    #     print(f"EL animal llamado {animal.getDescription()}")
    #     animal.HacerRuido()
    #     animal.comer()

    factura: Factura = Factura()
    factura.addHeader(Header(datetime.now(), "cod1-1", "logo.gif"))
    factura.addBillingInformation(BillingInformation("Orlo Corp", "Orlando Pally", "Barrio Colquiri", "4308441", "lando@lando.com"))
    factura.addShippingInformation(ShippingInformation())
    factura.addDetail(Product())
    factura.addDetail(Product())
    factura.addDetail(Product())

    print(factura.toString())


