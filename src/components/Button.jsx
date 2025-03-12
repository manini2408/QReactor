import { motion } from 'framer-motion';

const Button = ({ children, primary, ...props }) => {
  return (
    <motion.button
      className={`button ${primary ? 'primary' : 'secondary'}`}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      transition={{ duration: 0.2 }}
      {...props}
    >
      {children}
    </motion.button>
  );
};

export default Button; 