from aircraft_engine import AircraftEngine


def main():
    engines = [
        AircraftEngine("ENG-001", 120.0, 5000.0, 780.0),
        AircraftEngine("ENG-002", 150.0, 3200.0, 860.0),
        AircraftEngine("ENG-003", 0.0, 0.0, 400.0),
        AircraftEngine("ENG-004", 100.0, 4500.0, 820.0),
    ]

    print("      飞机发动机监控报告")
    for engine in engines:
        engine.display_info()


if __name__ == '__main__':
    main()
