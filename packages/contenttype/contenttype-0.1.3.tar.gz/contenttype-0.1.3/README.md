# Parse Content-Type Headers
> Python package for parsing Content-Type HTTP headers

## Usage

```python
from contenttype import ContentType

result = ContentType.parse('application/rss+xml; charset=utf-8')

result.type       # => 'application'
result.subtype    # => 'rss'
result.suffix     # => 'xml'
result.parameters # => {'charset': 'utf-8'}
result.charset    # => 'utf-8'
```
