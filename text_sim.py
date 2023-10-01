import curses

def drone_simulation(screen):
    curses.curs_set(0)  # 커서 숨김
    height, width = screen.getmaxyx()
    drone_pos = [width // 2, height // 2]

    while True:
        key = screen.getch()
        if key == curses.KEY_UP:
            drone_pos[1] -= 1
        elif key == curses.KEY_DOWN:
            drone_pos[1] += 1
        elif key == curses.KEY_LEFT:
            drone_pos[0] -= 1
        elif key == curses.KEY_RIGHT:
            drone_pos[0] += 1
        elif key == ord('q'):
            break

        screen.clear()
        screen.addch(drone_pos[1], drone_pos[0], 'D')
        screen.refresh()

curses.wrapper(drone_simulation)

