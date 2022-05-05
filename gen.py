#!/usr/bin/env python3

import base64
import sys

inner = 100
outer = 1000
frames = 1803
duration = '30s'

if len(sys.argv) < 2:
	print('Usage: ./gen.py image_path [image_type] > bounce.svg')
	quit()

avatar_path = sys.argv[1]
if len(sys.argv) == 3:
	avatar_type = sys.argv[2]
else:
	avatar_type = avatar_path.split('.').pop()

x = 0
y = 0

vx = 3
vy = 2

times = [0]
values = [[x, y]]
for i in range(0, frames):
	x += vx
	y += vy

	changed = False
	if x < 0 or x + inner >= outer:
		changed = True
		vx = -vx
	if y < 0 or y + inner >= outer:
		changed = True
		vy = -vy
	
	if changed:
		times.append(i / float(frames))
		values.append([x, y])

times_str = ';'.join([format(t, '.2f') for t in times])
values_str = ';'.join([f'{v[0]},{v[1]}' for v in values])

with open(avatar_path, 'rb') as fp:
	avatar_bin = fp.read()

avatar_b64 = base64.b64encode(avatar_bin).decode()

print(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{outer}" height="{outer}" viewBox="0 0 {outer} {outer}">
<defs>
	<clipPath id="circle">
		<circle cx="{inner / 2}" cy="{inner / 2}" r="{inner / 2}" fill="#FFFFFF" />
	</clipPath>
</defs>
<image width="{inner}" height="{inner}" href="data:image/{avatar_type};base64,{avatar_b64}" clip-path="url(#circle)">
	<animateTransform
		attributeName="transform"
		type="translate"
		dur="{duration}"
		repeatCount="indefinite"
		values="{values_str}"
		keyTimes="{times_str}"
	/>
</image>
</svg>''')

