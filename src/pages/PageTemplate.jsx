import { motion } from 'framer-motion';
import { ScrollReveal } from '../components/animations/ScrollReveal';

// Use this as a template for each page
const PageTemplate = ({ title, children }) => {
  return (
    <motion.div
      className="page"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.4 }}
    >
      <motion.h1
        className="page-title"
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2, duration: 0.6 }}
      >
        {title}
      </motion.h1>
      
      {children}
    </motion.div>
  );
};

export default PageTemplate; 