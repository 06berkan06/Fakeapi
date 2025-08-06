from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import datetime


class KullaniciBase(BaseModel):
    kullanici_adi: str = Field(..., min_length=3, max_length=50,
                               description="Kullanıcı adı")
    parola: str = Field(..., min_length=6, max_length=100,
                        description="Parola")

    @validator('kullanici_adi')
    def kullanici_adi_gecerli(cls, v):
        if not v.strip():
            raise ValueError('Kullanıcı adı boş olamaz')
        return v.strip()

    @validator('parola')
    def parola_gecerli(cls, v):
        if not v.strip():
            raise ValueError('Parola boş olamaz')
        return v.strip()


class KullaniciCreate(KullaniciBase):
    pass


class KullaniciLogin(KullaniciBase):
    pass


class KullaniciResponse(BaseModel):
    id: int
    kullanici_adi: str
    admin: bool

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    success: bool
    message: str
    kullanici: Optional[KullaniciResponse] = None


class AracBase(BaseModel):
    isim: str = Field(..., min_length=2, max_length=100,
                      description="Araç ismi")
    kategori: str = Field(..., min_length=2, max_length=50,
                         description="Araç kategorisi")
    model: str = Field(..., min_length=1, max_length=50,
                      description="Araç modeli")
    yil: int = Field(..., ge=1950, le=2024, description="Araç yılı")
    aciklama: Optional[str] = None
    resim_url: Optional[str] = None

    @validator('isim')
    def isim_gecerli(cls, v):
        if not v.strip():
            raise ValueError('Araç ismi boş olamaz')
        return v.strip()

    @validator('kategori')
    def kategori_gecerli(cls, v):
        if not v.strip():
            raise ValueError('Kategori boş olamaz')
        return v.strip()

    @validator('model')
    def model_gecerli(cls, v):
        if not v.strip():
            raise ValueError('Model boş olamaz')
        return v.strip()

    @validator('yil')
    def yil_gecerli(cls, v):
        current_year = datetime.now().year
        if v < 1950:
            raise ValueError('Araç yılı 1950\'den eski olamaz')
        if v > current_year:
            raise ValueError(f'Araç yılı {current_year} yılından yeni olamaz')
        return v


class AracCreate(AracBase):
    pass


class AracUpdate(AracBase):
    favori: Optional[bool] = None


class AracResponse(AracBase):
    id: int
    favori: bool

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str
    success: bool
    data: Optional[dict] = None


__all__ = [
    "KullaniciBase", "KullaniciCreate", "KullaniciLogin", 
    "KullaniciResponse", "LoginResponse",
    "AracBase", "AracCreate", "AracUpdate",
    "AracResponse", "MessageResponse"
]
