/**
 * Abstract driving an analog meter to be driven by PWM,
 * and do the math to calculate the right PWM values.
 */
class Meter {
	private:
		/**
		 * An analogWrite of analogFullScale*255*value wil set the meter
		 * to value fraction of its full range.
		 */
		const float analogFullScale;
		const int pin;
	public:
		Meter(int pin, float maxCurrentAmps,
			float seriesResistance, float internalResistance=0.0);
		void setup();
		void setValue(float value);
};

