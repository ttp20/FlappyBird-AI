import pygame
import neat

from settings import Settings
from birds import Bird
from ground import Ground
from pipes import Pipe

def draw_screen(screen, birds, pipes, ground, score, gen):
    screen.blit(Settings.BACKGROUNG_IMG, (0,0))

    for bird in birds:
        bird.draw(screen)

    for pipe in pipes:
        pipe.draw(screen)

    score_text = Settings.FONT.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_text, (Settings.SCREEN_WIDTH - 10 - score_text.get_width(), 10))

    gen_text = Settings.FONT.render(f"Generation: {gen}", True, (255,255,255))
    screen.blit(gen_text, (10, 10))

    ground.draw(screen)

    pygame.display.update()

def main_and_fitness(genomes, config):
    # bird = Bird(230,350)
    Settings.GEN += 1
    birds = []
    nets = []
    ge = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    ground = Ground(730)
    pipes = [Pipe(700)]

    score = 0
    running = True
    screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    while running:
        clock.tick(30)
        # bird.move()

        add_pipe = False
        removed_pipes = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                removed_pipes.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            # for g in ge:
            #     g.fitness += 1
            pipes.append(Pipe(600))

        for removed in removed_pipes:
            pipes.remove(removed)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() > ground.y or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
        
        pipe_idx = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_idx = 1
        else:
            running = False
            break
        
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_idx].height), abs(bird.y - pipes[pipe_idx].bottom)))

            if output[0] > 0.5:
                bird.jump()

        ground.move()

        draw_screen(screen, birds, pipes, ground, score, Settings.GEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main_and_fitness, 50)