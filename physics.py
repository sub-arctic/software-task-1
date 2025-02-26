import vec2


def calculate_velocity(data_points):
    if len(data_points) < 2:
        return vec2.Vec2(0, 0)

    dp1 = data_points[-2]
    dp2 = data_points[-1]

    dx = dp2.x - dp1.x
    dy = dp2.y - dp1.y

    dt = (dp2.time - dp1.time) / 1_000_000_000

    if dt > 0:
        vx = dx / dt
        vy = dy / dt

        max_velocity = 800
        speed = (vx**2 + vy**2) ** 0.5

        if speed > max_velocity:
            vx = (vx / speed) * max_velocity
            vy = (vy / speed) * max_velocity

        return vec2.Vec2(vx, vy)
    else:
        return vec2.Vec2(0, 0)
