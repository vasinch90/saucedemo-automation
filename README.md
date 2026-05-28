# SauceDemo Automation

![CI](https://github.com/vasinch90/saucedemo-automation/actions/workflows/ci.yml/badge.svg)

Selenium + pytest automation project สำหรับ SauceDemo e-commerce

## Tech Stack
- Python 3.x
- Selenium 4
- pytest
- Page Object Model
- GitHub Actions CI/CD

## Test Coverage
| Feature | Tests |
|---|---|
| Login | 10 |
| Add to Cart | 3 |
| Checkout | 3 |
| Sort | 4 |
| **Total** | **20** |

## Run tests
\`\`\`bash
pip install -r requirements.txt
pytest tests/ -v
\`\`\`