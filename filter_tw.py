import requests
import yaml
import base64

# 订阅链接
sub_url = "https://imperialb.in/r/eav0dzoa"

# 获取订阅内容
response = requests.get(sub_url)
if response.status_code != 200:
    print("❌ 订阅链接获取失败，请检查 URL 是否正确")
    exit(1)

raw_data = response.text

# 检查是否是 Base64 编码（部分 Clash 订阅会这样）
try:
    decoded_data = base64.b64decode(raw_data).decode("utf-8")
    print("✅ 订阅内容已成功解码 Base64")
except Exception:
    decoded_data = raw_data

# 解析 YAML
try:
    config = yaml.safe_load(decoded_data)
    if not isinstance(config, dict) or "proxies" not in config:
        raise ValueError("❌ 解析 YAML 失败，可能格式不正确")
except Exception as e:
    print(f"❌ YAML 解析失败: {e}")
    exit(1)

# 过滤台湾（TW）节点
filtered_proxies = [p for p in config["proxies"] if isinstance(p, dict) and ("TW" in p.get("name", "") or "台湾" in p.get("name", ""))]

# 生成新的 YAML 配置
config["proxies"] = filtered_proxies
for group in config.get("proxy-groups", []):
    group["proxies"] = [p["name"] for p in filtered_proxies if p["name"] in group.get("proxies", [])]

# 保存到 taiwan.yaml 文件
with open("taiwan.yaml", "w", encoding="utf-8") as f:
    yaml.dump(config, f, allow_unicode=True)

print("✅ 台湾节点筛选完成，已生成 taiwan.yaml")
