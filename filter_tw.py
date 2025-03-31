import requests
import yaml

# 订阅地址
sub_url = "https://imperialb.in/r/eav0dzoa"

# 获取订阅内容
response = requests.get(sub_url)
if response.status_code != 200:
    print("❌ 订阅链接获取失败，请检查 URL 是否正确")
    exit(1)

# 解析 YAML
config = yaml.safe_load(response.text)

# 过滤台湾（TW）节点
filtered_proxies = [p for p in config["proxies"] if "TW" in p["name"] or "台湾" in p["name"]]

# 生成新的 YAML 配置
config["proxies"] = filtered_proxies
for group in config["proxy-groups"]:
    group["proxies"] = [p["name"] for p in filtered_proxies if p["name"] in group["proxies"]]

# 保存到 taiwan.yaml 文件
with open("taiwan.yaml", "w", encoding="utf-8") as f:
    yaml.dump(config, f, allow_unicode=True)

print("✅ 台湾节点筛选完成，已生成 taiwan.yaml")
