package task

import (
	"context"
	"encoding/json"
	"fmt"
	"math"
	"math/rand/v2"
	"signal/config"
	"signal/log"
	"signal/timeoutrw"
	"strings"
)

const (
	newLine              = '\n'
	welcomeMsg           = "We've caught some signals but can't tell the difference between aliens and noise, help us identify which is which.\nSend us one of the options in response:\n- ALIEN\n- NOISE\n\n"
	winAccuracyThreshold = 0.9
)

func Task(ctx context.Context, rw *timeoutrw.TimeoutReadWriter) error {
	logger := log.Logger(ctx)
	cfg := config.GetConfig()

	if _, err := rw.WriteString(welcomeMsg); err != nil {
		return fmt.Errorf("error on write: %w", err)
	}

	correct := 0
	for i := 0; i < cfg.Levels; i++ {
		signal := GenerateSignal()

		if _, err := rw.WriteStringf(
			"[i = %d, correct = %d] Signal params:\n%s\nVerdict: ", i+1, correct, signal,
		); err != nil {
			return fmt.Errorf("error on write: %w", err)
		}

		resp, err := rw.ReadStringUntil(newLine)
		if err != nil {
			return fmt.Errorf("error on read: %w", err)
		}

		logger.Infof("received data: '%s'", resp)

		if signal.IsAlien && strings.TrimSpace(resp) == "ALIEN" {
			correct++
		} else if !signal.IsAlien && strings.TrimSpace(resp) == "NOISE" {
			correct++
		}
	}

	acc := float64(correct) / float64(cfg.Levels)
	if acc < winAccuracyThreshold {
		logger.Infof("losed, acc = %0.2f, threshold = %0.2f", acc, winAccuracyThreshold)
		if _, err := rw.WriteStringf("Loser! Your accuracy = %0.2f%%, no flag for you\n", acc*100); err != nil {
			return fmt.Errorf("error on write: %w", err)
		}
	} else {
		logger.Infof("losed, acc = %0.2f, threshold = %0.2f", acc, winAccuracyThreshold)
		if _, err := rw.WriteStringf("Gratz! Your accuracy = %0.2f%%, here is your flag: \n%s\n", acc*100, cfg.Flag); err != nil {
			return fmt.Errorf("error on write: %w", err)
		}
	}

	return nil
}

type Signal struct {
	Frequency      float64 `json:"frequency"`       // p1: частота (ГГц)
	Amplitude      float64 `json:"amplitude"`       // p2: амплитуда (dB)
	PulseDuration  float64 `json:"pulse_duration"`  // p3: длительность импульса (мс)
	Periodicity    float64 `json:"periodicity"`     // p4: периодичность (сек)
	ReceptionAngle float64 `json:"reception_angle"` // p5: угол приёма (°)
	NoiseTemp      float64 `json:"noise_temp"`      // p6: шумовая температура (K)
	Distance       float64 `json:"distance"`        // p7: расстояние (св. годы)
	SpectralClass  float64 `json:"spectral_class"`
	P              float64 `json:"p"`
	D              float64 `json:"d"`
	IsAlien        bool    `json:"-"`
}

func (s Signal) String() string {
	signalJson, err := json.Marshal(s)
	if err != nil {
		panic(fmt.Sprintf("failed to marshal signal: %v", err))
	}

	return string(signalJson)
}

const (
	noiseLevel = 2.0
)

func GenerateSignal() Signal {
	// Параметры, влияющие на событие
	p1 := rand.NormFloat64()*2 + 5
	p2 := rand.ExpFloat64() / 0.5
	p3 := rand.Float64() * 2 * math.Pi
	p4 := math.Exp(rand.NormFloat64()*0.5 + 1)
	p5 := (rand.Float64() - 0.5) * 20
	p6 := rand.Float64() * 50
	p7 := rand.NormFloat64()*10 + 20

	// Параметры-шумы (не влияют на сигнал)
	p8 := rand.NormFloat64() * 154
	p9 := (rand.Float64() - 0.5) * -50
	p10 := rand.ExpFloat64() / 0.432

	// Вычисляем сигнал
	signal := math.Pow(p1, p2/10.0)*math.Log(p3+1)/(1+math.Abs(math.Sin(p4))) + p5*p6 - math.Sqrt(p7)
	noise := (rand.Float64() - 0.5) * 2 * noiseLevel
	signal = signal + noise

	threshold := 50.0 + 5*math.Sin(p1) // Порог "плавает"

	s := Signal{
		Frequency:      p1,
		Amplitude:      p2,
		PulseDuration:  p3,
		Periodicity:    p4,
		ReceptionAngle: p5,
		NoiseTemp:      p6,
		Distance:       p7,
		SpectralClass:  p8,
		P:              p9,
		D:              p10,
		IsAlien:        signal > threshold+noise,
	}

	if rand.Float64() < 0.05 {
		s.IsAlien = !s.IsAlien
	}

	return s
}
