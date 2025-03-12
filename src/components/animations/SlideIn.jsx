import { motion } from 'framer-motion';

export const SlideIn = ({ 
  children, 
  direction = "up", 
  delay = 0, 
  duration = 0.5,
  distance = 50,
  ...props 
}) => {
  const directionMap = {
    up: { y: distance },
    down: { y: -distance },
    left: { x: distance },
    right: { x: -distance }
  };
  
  const initial = directionMap[direction];
  
  return (
    <motion.div
      initial={{ ...initial, opacity: 0 }}
      animate={{ x: 0, y: 0, opacity: 1 }}
      transition={{ duration, delay }}
      {...props}
    >
      {children}
    </motion.div>
  );
}; 