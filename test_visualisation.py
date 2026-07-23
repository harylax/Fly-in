import pygame
from map_model import Map, Color
from simulation import Simulation

pygame.init()

WIDTH = 1200
HEIGHT = 600
TURN_DURATION_MS = 2000  # 2 seconde par tour

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation drones")
clock = pygame.time.Clock()

# --- Assets ---
bg = pygame.image.load('isometric-city-bg-1600x800-darker.png')
BACKGROUND = pygame.transform.smoothscale(bg, (WIDTH, HEIGHT))
drone_img = pygame.image.load('drone-isometric-facing-right.png')
DRONE_IMG = pygame.transform.smoothscale(drone_img, (50, 50))

font = pygame.font.SysFont(None, 22)

# --- Simulation ---
# game_map = Map('maps/easy/01_linear_path.txt')
# game_map = Map('maps/easy/02_simple_fork.txt')
# game_map = Map('maps/easy/03_basic_capacity.txt')
# game_map = Map('maps/medium/01_dead_end_trap.txt')
game_map = Map('maps/medium/02_circular_loop.txt')
simulation = Simulation(game_map)
# simulation.linear_solve()
simulation.circular_solve()
drones_moves = simulation.drones_moves

# --- Positionnement des hubs sur l'écran ---
MARGIN = 150
xs = [hub.x for hub in game_map.hubs]
ys = [hub.y for hub in game_map.hubs]
min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)


def to_screen(x: int, y: int) -> tuple[int, int]:
    # évite division par zéro si tous les x ou y sont identiques
    range_x = (max_x - min_x) or 1
    range_y = (max_y - min_y) or 1
    sx = MARGIN + (x - min_x) / range_x * (WIDTH - 2 * MARGIN)
    sy = MARGIN + (y - min_y) / range_y * (HEIGHT - 2 * MARGIN)
    return int(sx), int(sy)


hub_positions: dict[str, tuple[int, int]] = {
    hub.name: to_screen(hub.x, hub.y) for hub in game_map.hubs
}


# --- Dessin statique : fond, connexions, hubs ---
def draw_static() -> None:
    screen.blit(BACKGROUND, (0, 0))

    for conn in game_map.connections:
        if conn.origin and conn.destination:
            p1 = hub_positions[conn.origin.name]
            p2 = hub_positions[conn.destination.name]
            pygame.draw.line(screen, Color.white.rgb, p1, p2, 3)

    for hub in game_map.hubs:
        pos = hub_positions[hub.name]
        pygame.draw.circle(screen, hub.color.rgb, pos, 20)
        label = font.render(hub.name, True, (255, 255, 255))
        screen.blit(label, (pos[0] - label.get_width() // 2, pos[1] - 40))


# --- Offset pour éviter que plusieurs drones sur le même hub se superposent ---
def offset_for_index(i: int, total: int) -> tuple[int, int]:
    if total <= 1:
        return (0, 0)
    import math
    angle = (2 * math.pi / total) * i
    radius = 18
    return (int(radius * math.cos(angle)), int(radius * math.sin(angle)))


# --- État de l'animation ---
current_turn = 0
progress_ms = 0
paused = True
running = True

max_turn = len(drones_moves) - 1

while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                paused = not paused

    if not paused and current_turn < max_turn:
        progress_ms += dt
        if progress_ms >= TURN_DURATION_MS:
            progress_ms = 0
            current_turn += 1

    draw_static()

    # progression 0..1 entre l'état "current_turn" et "current_turn+1"
    t = min(progress_ms / TURN_DURATION_MS, 1.0) if current_turn < max_turn else 0.0

    prev_state = drones_moves[current_turn]
    next_state = drones_moves[min(current_turn + 1, max_turn)]

    # compter combien de drones partagent chaque hub à cet instant (pour l'offset)
    hub_counts: dict[str, int] = {}
    for _, hub_name in next_state:
        hub_counts[hub_name] = hub_counts.get(hub_name, 0) + 1
    hub_seen: dict[str, int] = {}

    for (drone_id, from_hub), (_, to_hub) in zip(prev_state, next_state):
        p1 = hub_positions[from_hub]
        p2 = hub_positions[to_hub]

        x = p1[0] + (p2[0] - p1[0]) * t
        y = p1[1] + (p2[1] - p1[1]) * t

        idx = hub_seen.get(to_hub, 0)
        hub_seen[to_hub] = idx + 1
        ox, oy = offset_for_index(idx, hub_counts.get(to_hub, 1))

        rect = DRONE_IMG.get_rect(center=(int(x) + ox, int(y) + oy))
        screen.blit(DRONE_IMG, rect)

        id_label = font.render(f"D{drone_id}", True, (255, 255, 0))
        screen.blit(id_label, (rect.x, rect.y - 15))

    turn_label = font.render(
        f"Turn {current_turn}/{max_turn}" + ("  [PAUSE]" if paused else ""),
        True, (255, 255, 255)
    )
    screen.blit(turn_label, (10, 10))

    pygame.display.flip()

pygame.quit()
