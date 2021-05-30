from bodies import *

def main():
    BODIES = 10
    board = Board(1000, 700)
    board.set_up()

    bodies = [Planet(mass=np.random.uniform(100, 1000),
                     x=np.random.uniform(0, 1000),
                     y=np.random.uniform(0, 700),
                     v=np.array([np.random.uniform(-1, 1), np.random.uniform(-1, 1)]))
              for _ in range(BODIES)]

    sun = Star(mass=10000.0,
               x=500.0,
               y=350.0)

    other_bodies = bodies[:]
    other_bodies.append(sun)

    been_there = list()
    timer = 0
    stoper = 10000
    while board.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                board.terminate()

        if timer > stoper:
            board.terminate()

        board.fill(been_there)
        for current_body in bodies:
            combined_forces = np.zeros(2)
            for other_body in other_bodies:
                if current_body is other_body:
                    continue
                combined_forces += current_body.get_force(other_body)
            current_body.change_speed(combined_forces)
            current_body.change_position()

            if len(been_there) > 3000:
                been_there.pop(0)
            been_there.append(tuple(current_body.position))

            board.draw(current_body)

        board.draw(sun)
        pygame.display.update()
        timer += 1
    pygame.quit()



if __name__ == '__main__':
    main()

