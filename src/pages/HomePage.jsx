import { motion } from 'framer-motion';
import { ScrollReveal } from '../components/animations/ScrollReveal';
import PageTemplate from './PageTemplate';

const HomePage = () => {
  return (
    <PageTemplate title="Welcome">
      {/* Hero Section */}
      <section className="hero">
        <motion.div 
          className="hero-content"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.8 }}
        >
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.8 }}
          >
            Your Compelling Headline
          </motion.h2>
          
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.7, duration: 0.8 }}
          >
            A brief description of your services or value proposition.
          </motion.p>
          
          <motion.button
            className="cta-button"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.9, duration: 0.5 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Get Started
          </motion.button>
        </motion.div>
      </section>
      
      {/* Features Section */}
      <section className="features">
        <ScrollReveal>
          <h3>Our Features</h3>
        </ScrollReveal>
        
        <div className="feature-grid">
          {[1, 2, 3].map((item, i) => (
            <ScrollReveal
              key={i}
              delay={i * 0.1}
              direction={i % 2 === 0 ? "left" : "right"}
            >
              <div className="feature-card">
                <motion.div 
                  className="feature-icon"
                  whileHover={{ rotate: 5, scale: 1.1 }}
                  transition={{ type: "spring", stiffness: 300 }}
                >
                  {/* Icon */}
                </motion.div>
                <h4>Feature {item}</h4>
                <p>Description of this amazing feature that your users will love.</p>
              </div>
            </ScrollReveal>
          ))}
        </div>
      </section>
      
      {/* Testimonials */}
      <section className="testimonials">
        <ScrollReveal>
          <h3>What Our Clients Say</h3>
        </ScrollReveal>
        
        <div className="testimonial-slider">
          {[1, 2, 3].map((testimonial, i) => (
            <ScrollReveal
              key={i}
              delay={i * 0.15}
              direction="up"
            >
              <motion.div 
                className="testimonial"
                whileHover={{ y: -5, boxShadow: "0 10px 20px rgba(0,0,0,0.1)" }}
              >
                <p>"This service exceeded my expectations and transformed how I work."</p>
                <div className="testimonial-author">
                  <div className="avatar"></div>
                  <span>Client Name {testimonial}</span>
                </div>
              </motion.div>
            </ScrollReveal>
          ))}
        </div>
      </section>
    </PageTemplate>
  );
};

export default HomePage; 