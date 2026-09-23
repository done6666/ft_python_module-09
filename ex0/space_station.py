# Egzersiz 0 - uzay istasyonu verisi
# BaseModel ve Field ile alan kısıtlarını doğruluyorum

from datetime import datetime

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):

    # uzunluk ve aralık kısıtlarını Field ile verdim,
    # pydantic örnek oluşturulurken hepsini kontrol ediyor
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)

    # string tarih verirsem pydantic kendisi datetime'a çeviriyor
    last_maintenance: datetime

    # değer verilmezse varsayılanlar geçerli
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def show_station(station: SpaceStation) -> None:
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    status = "Operational" if station.is_operational else "Non-operational"
    print(f"Status: {status}")


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")

    # geçerli kayıt sorunsuz oluşuyor
    try:
        station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2024, 6, 1, 10, 30),
            is_operational=True,
        )
        print("Valid station created:")
        show_station(station)
    except ValidationError:
        print("Failed to create valid station")
    print()
    print("========================================")

    # crew_size 20'den büyük olunca ValidationError geliyor,
    # ilk hata mesajını yazdırıyorum
    try:
        SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=25,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2024, 6, 1, 10, 30),
            is_operational=True,
        )
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
