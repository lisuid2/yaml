import requests
import yaml
import base64

# 订阅地址
sub_url = "https://imperialb.in/r/eav0dzoa"

# 获取订阅内容
response = requests.get(sub_url)
if response.status_code != 200:
    print("❌ 订阅获取失败，请检查 URL")
    exit(1)

raw_data = response.text.strip()

# 尝试 Base64 解码
try:
    decoded_data = base64.b64decode(raw_data).decode("utf-8")
    if "proxies" in decoded_data or "port" in decoded_data:  
        print("✅ Base64 解码成功")
        raw_data = decoded_data
except Exception:
    print("⚠️ 不是 Base64 编码，直接解析 YAML")

# **尝试解析 YAML**
try:
    config = yaml.safe_load(raw_data)
    if not isinstance(config, dict) or "proxies" not in config:
        raise ValueError("❌ 解析 YAML 失败，可能格式不对")
except Exception as e:
    print(f"❌ YAML 解析失败: {e}")
    exit(1)

# **筛选台湾（TW）节点**
filtered_proxies = [p for p in config.get("proxies", []) if isinstance(p, dict) and ("TW" in p.get("name", "") or "台湾" in p.get("name", ""))]

if not filtered_proxies:
    print("⚠️ 没有找到台湾节点")
    exit(0)

# **生成新的 YAML**
config["proxies"] = filtered_proxies
for group in config.get("proxy-groups", []):
    group["proxies"] = [p["name"] for p in filtered_proxies if p["name"] in group.get("proxies", [])]

# **保存到 `taiwan.yaml`**
with open("taiwan.yaml", "w", encoding="utf-8") as f:
    yaml.dump(config, f, allow_unicode=True)

print("✅ 台湾节点筛选完成，已生成 `taiwan.yaml`")
