class AircraftEngine:
    """飞机发动机监控类"""

    def __init__(self, engine_id, fuel_flow, thrust, temperature):
        self.engine_id = engine_id          # 发动机编号 (字符串)
        self.fuel_flow = fuel_flow          # 燃料流量 kg/h (浮点数)
        self.thrust = thrust                # 推力输出 N (浮点数)
        self.temperature = temperature      # 工作温度 °C (浮点数)

    def calc_efficiency(self):
        """计算燃油效率（推力/燃料流量），燃料流量为0时返回None"""
        if self.fuel_flow == 0:
            return None
        return self.thrust / self.fuel_flow

    def check_status(self):
        """判断发动机是否处于安全运行状态"""
        problems = []

        if self.temperature >= 850:
            problems.append("温度过高")

        efficiency = self.calc_efficiency()
        if efficiency is not None and efficiency <= 30:
            problems.append("效率偏低")

        if not problems:
            return "正常运行"
        return "、".join(problems)

    def display_info(self):
        """打印发动机详细运行信息"""
        efficiency = self.calc_efficiency()
        eff_str = f"{efficiency:.2f} N/(kg/h)" if efficiency is not None else "无法计算（燃料流量为0）"

        print(f"{'=' * 40}")
        print(f"  发动机编号：{self.engine_id}")
        print(f"  燃料流量：{self.fuel_flow} kg/h")
        print(f"  推力输出：{self.thrust} N")
        print(f"  工作温度：{self.temperature} °C")
        print(f"  燃油效率：{eff_str}")
        print(f"  状态检查：{self.check_status()}")
        print(f"{'=' * 40}")



