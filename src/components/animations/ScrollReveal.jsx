import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

export const ScrollReveal = ({ 
  children, 
  threshold = 0.1,
  triggerOnce = true,
  direction = "up",
  duration = 0.7,
  distance = 50,
  ...props 
}) => {
  const [ref, inView] = useInView({
    triggerOnce,
    threshold
  });
  
  const directionMap = {
    up: { y: distance },
    down: { y: -distance },
    left: { x: distance },
    right: { x: -distance }
  };
  
  const initial = directionMap[direction];
  
  return (
    <motion.div
      ref={ref}
      initial={{ ...initial, opacity: 0 }}
      animate={inView ? { x: 0, y: 0, opacity: 1 } : { ...initial, opacity: 0 }}
      transition={{ duration }}
      {...props}
    >
      {children}
    </motion.div>
  );
}; 